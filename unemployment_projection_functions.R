# unemployment_projection_functions.R
#
# Helper functions to map exposure into unemployment/NILF paths
# using simple discrete-time dynamics.

simulate_unemployment_path <- function(
  exposure,
  activation,
  unemp_ratio = 0.29,
  reemployment_rate = 0.15,
  T = 20
) {
  displaced_total <- exposure * activation
  displaced_per_year <- displaced_total / T

  unemployment <- numeric(T)
  nilf <- numeric(T)

  current_unemp <- 0
  current_nilf <- 0

  for (t in 1:T) {
    new_unemp <- displaced_per_year * unemp_ratio
    new_nilf <- displaced_per_year * (1 - unemp_ratio)

    reemp <- reemployment_rate * current_unemp

    current_unemp <- current_unemp + new_unemp - reemp
    current_nilf <- current_nilf + new_nilf

    unemployment[t] <- current_unemp
    nilf[t] <- current_nilf
  }

  tibble::tibble(
    year = 1:T,
    unemployment = unemployment,
    nilf = nilf
  )
}
