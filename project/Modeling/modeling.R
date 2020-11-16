# Limpia el espacio de trabajo, las parcelas y la consola
rm(list = ls())
if(!is.null(dev.list())) dev.off()
cat("\014") 

library(lmtest)
library(tidyverse)
library(caret)
library(regclass)
library(sandwich)
library(robustbase)
library(modelr)
library(broom)
library(lmvar)

# install.packages('lmvar')
setwd("/home/rcmartinb/DS4A")

save.image()
load('.RData')

#leer transformar datos
ofertas <- read.table("ofertas.csv", sep=',',header=T)
names(ofertas)


cat_cols <- c('preczhf','oft_tipo_inmueble', 'oft_tipo_norma_juridica','oia_tiene_ascensor','loccodigo',
              'locnombre','nombre_barrio','suelo', 'actividad','tratamiento_urb','topografia','serpub',
              'serpub_tipo','serpub_especif','via','clase_via','estado_via','influencia_via','actividad_economica',
              'actividad_economica_tipo','tipo_segun_actividad','cp_terr_ar')

ofertas[cat_cols] <- lapply(ofertas[cat_cols], factor)

ignore = c('oft_codigo', 'lotcodigo', 'manzana_id', 'prevetustz', 'oia_tiene_ascensor', 'oic_valor_adm', 'oic_valor_anexos', 
           'preczhf', 'codigo_con', 'codigo_res', 'loccodigo', 'barmanpre', 'nombre_barrio', 'locnombre')

ofertas <- ofertas[ , !(names(ofertas) %in% ignore)]

delete.na <- function(df, n=0) {
  df[rowSums(is.na(df)) <= n,]
}
ofertas <- delete.na(ofertas)

## outliers
ofertas$sqrt_oic_area_construccion <- sqrt(ofertas$oic_area_construccion)
ofertas$sqrt_oic_area_terreno <- sqrt(ofertas$oic_area_terreno)
ofertas <- filter(ofertas,log_vfventa2020 <22,log_vfventa2020>16,sqrt_oic_area_terreno<50,sqrt_oic_area_construccion<50)
## MODEL ##
#OLS
formula <- (log(vfventa2020) ~ estrato + x  + y + topografia + d_tm + d_col + oft_tipo_inmueble +
              d_highway + oft_tipo_norma_juridica + sqrt(oic_area_terreno) + oia_cant_garajes +
              cp_terr_ar + suelo + d_p_tm + d_bom + d_mus +
               actividad_economica_tipo  + dm_sitp + sqrt(oic_area_construccion))
#estado via clase_via
m.OLS <- lm(formula,data=ofertas, y=TRUE,x=TRUE)
MSE(m.OLS)
summary(m.OLS)


#NORMALITY
hist(residuals(m.OLS))
ks.test(residuals(m.OLS),'pnorm',mean(residuals(m.OLS)),sd(residuals(m.OLS)))
#Heteroced
bptest(m.OLS)
#multicol
VIF(m.OLS)
#autocorrelation
dwtest(m.OLS)
AIC(m.OLS)

mod_data <- data.frame( vfv2020 =log(ofertas$vfventa2020),resi=m.OLS$residuals)


ofertas$resi <- residuals(m.OLS)
### WLS ###

wts     <- 1/fitted( lm(abs(residuals(m.OLS))~fitted(m.OLS)) )^2


m.WLS <- lm(formula,data=ofertas, weights=wts, y=TRUE,x=TRUE)
install.packages('MLmetrics')
library(MLmetrics)
summary(m.WLS)
wlssum <- summary(m.WLS)
write.csv(data.frame(wlssum$coefficients),file='WLS_result.csv')
AIC(m.WLS)
BIC(m.WLS)
MSE(m.WLS)
MSE(ofertas$log_vfventa2020,m.OLS$fitted.values)

length(m.WLS$residuals)
#NORMALITY
hist(residuals(m.WLS))
ks.test(residuals(m.WLS),'pnorm',mean(residuals(m.WLS)),sd(residuals(m.WLS)))
#Heteroced
bptest(m.WLS)
#multicol
VIF(m.WLS)
#autocorrelation
dwtest(m)

cv.lm(m.WLS, log = TRUE)


# GLS

formula.varfunc <- (log(resi^2) ~ log(estrato) + log(x)  + log(y) + topografia + log(d_tm) + log(d_col) + oft_tipo_inmueble +
                              log(d_highway) + oft_tipo_norma_juridica + log(sqrt(oic_area_terreno)) + log(oia_cant_garajes)+
                                      cp_terr_ar + suelo + log(d_p_tm) + log(d_bom) + log(d_mus) +
                                      actividad_economica_tipo  + log(dm_sitp) + log(sqrt(oic_area_construccion)))
varfunc.ols <- lm(formula.varfunc,data=ofertas)
summary(varfunc.ols)
###BOOTSTRAP
resamples <- 100

boot_ofertas <- ofertas %>% 
  modelr::bootstrap(resamples)
boot_ofertas

(
  boot_lin_reg <- boot_ofertas %>% 
    mutate(regressions = 
             map(strap, 
                 ~lm(formula , 
                     data = .))) 
)

(
  tidied <- boot_lin_reg %>% 
    mutate(tidy_lm = 
             map(regressions, broom::tidy))
)

tidied$tidy_lm[[1]]

summary(tidied$regressions[[1]])
formula
list_mods <- tidied %>% 
  pull(tidy_lm)

mods_df <- map2_df(list_mods, 
                   seq(1, resamples), 
                   ~mutate(.x, resample = .y))
head(mods_df, 25)
m
(
  r.std.error <- mods_df %>% 
    group_by(term) %>% 
    summarise(r.std.error = sd(estimate))
)
m %>% 
  broom::tidy() %>% 
  full_join(r.std.error) %>% 
  select(term, estimate, std.error, r.std.error)