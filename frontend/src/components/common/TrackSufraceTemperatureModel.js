/* eslint-disable import/prefer-default-export */
// review: https://doi.org/10.3390/app11093794

export const calculateTrackSurfaceTemperatureDegCKhan2019 = (
  airDegC,
  windSpeedMetersSeconds,
  humidityPercent,
  solarRadiationWattPerMetersSquared,
) => {
  const asphaltFahrenheit = 41.51
    + 0.102 * windSpeedMetersSeconds
    + 1.71 * airDegC
    + 0.032 * humidityPercent
    - 0.029 * solarRadiationWattPerMetersSquared
    + 0.002 * airDegC * humidityPercent
    + 5.7 * (10 ** -4) * windSpeedMetersSeconds * solarRadiationWattPerMetersSquared
    + 0.0014 * solarRadiationWattPerMetersSquared
    + 4.09 * (10 ** -5) * (solarRadiationWattPerMetersSquared ** 2)
    - 1.15 * (10 ** -6) * airDegC * (solarRadiationWattPerMetersSquared ** 2);
  return (asphaltFahrenheit - 32) / 1.8;
  // source: https://doi.org/10.1016/j.jtte.2018.04.005
};

export const calculateTrackSurfaceTemperatureDegCHassan2004 = (airDegC) => -1.437 + 1.121 * airDegC;
// source: https://doi.org/10.1016/j.conbuildmat.2007.06.016
