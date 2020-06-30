/* eslint-disable import/prefer-default-export */

export const flattenNestedObjects = (inputObject) => {
  const outputArray = [];
  for (let i = 0; i < Object.keys(inputObject).length; i += 1) {
    outputArray.push(
      Object.assign(Object.values(inputObject)[i], { name: Object.keys(inputObject)[i] }),
    );
  }
  return outputArray;
};
export const processStateOfIntervalHours = (latest, interval, current, digits) => {
  const state = ((latest + interval - current) / interval) * 100;
  return Number.parseFloat(state.toPrecision(digits));
};
export const processLeftIntervalHours = (latest, interval, current, digits) => {
  const hoursLeft = latest + interval - current;
  return Number.parseFloat(hoursLeft.toPrecision(digits));
};
export const processLeftIntervalYears = (latestDate, digits) => {
  const latest = new Date(latestDate);
  const now = new Date();
  const start = new Date(latest.getFullYear(), 0, 0);
  const diff = now - start;
  const oneDay = 1000 * 60 * 60 * 24;
  const day = Math.floor(diff / oneDay);
  const daysLeft = 365 - day;

  return Number.parseFloat(daysLeft.toPrecision(digits));
};
export const processStateOfIntervalYears = (latestDate, digits) => {
  const latest = new Date(latestDate);
  const now = new Date();
  const start = new Date(latest.getFullYear(), 0, 0);
  const diff = now - start;
  const oneDay = 1000 * 60 * 60 * 24;
  const day = Math.floor(diff / oneDay);
  const state = (day / 365) * 100;

  return Number.parseFloat(state.toPrecision(digits));
};
