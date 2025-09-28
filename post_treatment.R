library(tidyverse)

#   This script requires several R packages. However, they
#   are not fully loaded with library(). Instead, functions
#   are accessed explicitly using the :: operator.
#
# Required packages (functions used):
#   - MASS        (fitdistr)
#   - qpcR        (akaike.weights)
#   - DescTools   (MeanCI, VarCI)
#   - vroom       (vroom)
#
# Example:
#   MASS::fitdistr(x, "normal")
#

# Loading data ----
parameter <- read_csv("initialization_of_simulations.csv")

# Functions for fit ----
distribution_fitting <- function(a_distribution){
    results <- tryCatch({
        mass_nb <- MASS::fitdistr(a_distribution, "negative binomial")
        mass_pois <- MASS::fitdistr(a_distribution, "poisson")
        size <- mass_nb$estimate[1]
        mu <- mass_nb$estimate[2]
        lambda <- mass_pois$estimate[1]
        akaike <- qpcR::akaike.weights(c(AIC(mass_nb, k = 2), AIC(mass_pois, k = 1)))
        poids_nb <- akaike$weights[1]
        poids_pois <- akaike$weights[2]
        results <- list(mu = mu |> unname(),
                        size = size |> unname(),
                        lambda = lambda |> unname(),
                        poids_nb = poids_nb,
                        poids_pois = poids_pois,
                        mass_nb_loglik = mass_nb$loglik |> unname(),
                        mass_pois_loglik = mass_pois$loglik |> unname()
        )
    },
    error=function(cond){
        return(list(mu = NA,
                    size = NA,
                    lambda = NA,
                    poids_nb = NA,
                    poids_pois = NA,
                    mass_nb_loglik = NA,
                    mass_pois_loglik = NA))
    })
    return(results)
}

analyse_one_run <- function(file, seed){
    run_data <- vroom::vroom(file) # |> 
    max_timer <- run_data |> group_by(timer, iteration) |> 
        summarise(n_te = sum(active_te) + sum(silent_te)) |> 
        filter(n_te == 0) |> 
        head(n = 1) |> 
        pull(timer)
    if(length(max_timer) > 0){
        timer_list <- run_data |> 
            filter(timer < max_timer) |> 
            select(timer) |> 
            distinct(timer) |> 
            pull()
    }else{
        timer_list <- run_data |> 
            select(timer) |> 
            distinct(timer) |> 
            pull() 
    }
    
    data_timer <- tibble()
    for(a_timer in timer_list){
        a_distribution <- run_data |> 
            filter(timer == a_timer) |>
            mutate(te = active_te + silent_te) |> 
            pull(te)
        ci_mean <- DescTools::MeanCI(a_distribution)
        ci_var <- DescTools::VarCI(a_distribution)
        temp_2 <- run_data |> 
            filter(timer == a_timer) |>
            summarise(temp = list(c(distribution_fitting(active_te + silent_te)))) |> 
            unnest_wider(temp) |> 
            rename_all(function(x) paste0("te_all_", x)) |>
            mutate(timer = a_timer) |> 
            mutate(te_all_mean_ci_lower = ci_mean[2] |> unname()) |> 
            mutate(te_all_mean_ci_upper = ci_mean[3] |> unname()) |> 
            mutate(te_all_var_ci_lower = ci_var[2] |> unname()) |> 
            mutate(te_all_var_ci_upper = ci_var[3] |> unname()) 
        data_timer <- bind_rows(data_timer, temp_2)
    } 
    
    fit_active_te <- data_timer
    
    mean_te <- run_data |>
        group_by(iteration, timer) |>  
        summarize(te_a_mean = mean(active_te),
                  te_s_mean = mean(silent_te),
                  all__mean = mean(active_te + silent_te),
                  te_all_var = var(active_te + silent_te),
                  nb_individual = max(id)) 
    
    with_te_the_end <- mean_te |> 
        ungroup() |> 
        filter(all__mean > 0) |> 
        filter(timer == max(timer)) 
    
    average_te_at_the_end <- pull(with_te_the_end, all__mean)
    timer_with_te_at_the_end <- pull(with_te_the_end, timer) 
    
    mean_te <- mean_te |> 
        ungroup() |> 
        mutate(max_timer_with_te = timer_with_te_at_the_end) |> 
        mutate(max_timer = max(timer)) |> 
        mutate(te_at_the_end = average_te_at_the_end) |> 
        mutate(seed = seed |> as.numeric()) |> 
        mutate(scenario = case_when(max_timer > max_timer_with_te ~ "SP",
                                    te_at_the_end > 300 ~ "CoExt_end",
                                    .default = "SE"
        ))
    
    all_data <- fit_active_te |>  
        left_join(mean_te, by = c("timer"))
    
    return(all_data)
}

# Data analysis ----
files <- list.files(pattern = "^data*", path = "./output/", full.names = TRUE)
evolution_data <- tibble()
for(file in files){
    seed <- str_extract(file, "[:digit:]+")
    data_file_evolution <- analyse_one_run(file = file,  seed = seed)
    evolution_data <- bind_rows(evolution_data, data_file_evolution)
}

now <- format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")
write_csv(evolution_data, paste0("output_", now, ".csv"))

# Visualisation ----
plot_for_scenario <- function(raw_data, scenario_filter, ratio = TRUE){
    long_data <- raw_data |> 
        filter(scenario == scenario_filter) |> 
        mutate(var_to_mean = te_all_var / all__mean)  |> 
        group_by(seed) |> 
        mutate(pourcentage = timer / max(timer + 1)) |> 
        pivot_longer(cols = c("all__mean", "te_all_var", "var_to_mean", "te_all_poids_nb", "te_all_size", "nb_individual"),
                     names_to = "variable",
                     values_to = "valeur") |> 
        mutate(variable = factor(variable,
                                 levels = c("nb_individual", "all__mean", "te_all_var", "var_to_mean", "te_all_poids_nb", "te_all_size"),
                                 labels = c("n", "bar(x)", "plain(Var) (x)", "plain(Var) (x) / bar(x)", "w[plain(nb)]", "k" ))) 
        
    if(ratio){
        fig <- long_data |> 
            ggplot() +
            aes(x = pourcentage,
                y = valeur) +
            geom_line() +
            scale_x_continuous(breaks = seq(0, 1, 0.25), labels = c(0, 0.25, "", 0.75, 1))+
            facet_grid(variable ~ seed, scales = "free", labeller = labeller(.rows = label_parsed)) +
            labs(x = "Temporal progression proportion",
                 y = "Values")
    } else {
        fig <- long_data |> 
            ggplot() +
            aes(x = timer,
                y = valeur) +
            geom_line() +
            facet_grid(variable ~ seed, scales = "free", labeller = labeller(.rows = label_parsed)) +
            labs(x = "Timer",
                 y = "Values")
    }
    return(fig)
}
    
plot_for_scenario(evolution_data, "SE")
plot_for_scenario(evolution_data, "CoExt_end")
plot_for_scenario(evolution_data, "SP")

plot_for_scenario(evolution_data, "SE", ratio = FALSE)
plot_for_scenario(evolution_data, "CoExt_end", ratio = FALSE)
plot_for_scenario(evolution_data, "SP", ratio = FALSE)
