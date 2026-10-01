# boston-air-quality-prediction

**Project description:**
Air quality in Boston changes based on the weather, the season, and local/regional emissions. This project will collect Boston's daily air pollutant and weather data, clean and combine it, create features, visualize patterns, and train models to predict tomorrow's Air Quality Index (AQI) from today's conditions.

**Timeline:**
- Week 1: Choose weather monitors, create download scripts, and assess data for completeness
- Week 2, 3: Clean and combine data, handle missing values, and create initial plots
- Week 4, 5: Create features, build baselines, and train first models
- Week 6, 7: Complete models, evaluate results, create visualizations, analyze errors
- Week 8: Update GitHub, Makefile, README, and record presentation

**Goals:**
Successfully predict tomorrow's Air Quality Index (AQI) based on today's weather conditions. This includes whether the AQI will be below 50 (good) or above 50 (moderate/unhealthy), as well as a prediction of the exact AQI score. 

Features to analyze
- today's PM2.5, Ozone, NO2, CO levels
- pollution levels from 1, 3, and 7 days ago
- temperature
- wind speed and direction
- humidity
- air pressure
- precipitation
- time of year (month/season)

**Data Collection Plan:**
Daily weather data will be sourced using the historical weather API from Open-Meteo with Boston's coordinates. Daily pollutant concentrations and AQI will be sourced using the daily data from EPA or their Air Quality System (AQS) API.
