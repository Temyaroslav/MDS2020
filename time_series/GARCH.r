library(rugarch)
library(lattice)
library(timeSeries)
library(quantmod)

df = read.csv("C:\\Users\\ytemchuk\\STUFF\\time_series\\data\\ibm_3h.csv")

windowLength = 3*252*2
refit_window = 3*252

foreLength = dim(df)[1] - windowLength
forecasts = vector(mode="character", length=foreLength)

final.order = c(0, 0, 0)

for (d in 0:foreLength){
  rets = df$ln_Close[(1+d):(windowLength+d)]
  
  if(d %% refit_window == 0){
    # fit the ARIMA model
    final.aic = Inf
    
    for (p in 0:5) for (q in 0:5){
      if(p == 0 && q == 0){
        next
      }
      
      arimaFit = tryCatch(arima(rets, order=c(p, 0, q)),
                          error=function( err ) FALSE,
                          warning=function( err ) FALSE)
      
      if( !is.logical( arimaFit ) ){
        current.aic = AIC(arimaFit)
        if (current.aic < final.aic){
          final.aic = current.aic
          final.order = c(p, 0, q)
          final.arima = arima(rets, order=final.order)
        }
      } else { next }
    }
  }
  
  # fit the GARCH model
  spec = ugarchspec(
    variance.model = list(garchOrder=c(1, 1)),
    mean.model=list(armaOrder=c(final.order[1], final.order[3]), include.mean=T),
    distribution.model="sged"
  )
  fit = tryCatch(ugarchfit(spec, rets, solver='hybrid'), 
                 error=function(e) e, 
                 warning=function(w) w)
  
  if(is(fit, "warning")) {
    forecasts[d+1] = paste(
      df$Date[windowLength+d], sapply(strsplit(forecasts[d], ","), `[`, 2), sep=","
    )
    print('Taking previous value')
    print(
      paste(
        df$Date[windowLength+d], sapply(strsplit(forecasts[d], ","), `[`, 2), sep=","
      )
    )
  } 
  else {
    fore = ugarchforecast(fit, n.ahead=1)
    ind = fore@forecast$seriesFor
    forecasts[d+1] = paste(
      df$Date[windowLength+d], ifelse(ind[1] < 0, -1, 1), sep=","
    )
    print(
      paste(df$Date[windowLength+d], ifelse(ind[1] < 0, -1, 1), sep=",")
    )
  }
 
}

write.csv(forecasts, file="forecasts.csv", row.names=FALSE)
