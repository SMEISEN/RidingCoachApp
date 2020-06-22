

const flattenNestedObjects = (inputObject) => {
  const outputArray = [];
  for (let i = 0; i < Object.keys(inputObject).length; i += 1) {
    outputArray.push(
      Object.assign(Object.values(inputObject)[i], {name: Object.keys(inputObject)[i]}),
    );
  }
  return outputArray;
};
const processStateOfIntervalHours = (latest, interval, current, digits) => {
  const state = ((latest + interval - current) / interval) * 100;
  return Number.parseFloat(state.toPrecision(digits));
};
const processLeftIntervalHours = (latest, interval, current, digits) => {
  const hours_left = latest + interval - current;
  return Number.parseFloat(hours_left.toPrecision(digits));
};
const processLeftIntervalYears = (latest_date, digits) => {
  const latest = new Date(latest_date);
  const now = new Date();
  const start = new Date(latest.getFullYear(), 0, 0);
  const diff = now - start;
  const oneDay = 1000 * 60 * 60 * 24;
  const day = Math.floor(diff / oneDay);
  const days_left = 365 - day;

  return Number.parseFloat(days_left.toPrecision(digits));
};
const processStateOfIntervalYears = (latest_date, digits) => {
  const latest = new Date(latest_date);
  const now = new Date();
  const start = new Date(latest.getFullYear(), 0, 0);
  const diff = now - start;
  const oneDay = 1000 * 60 * 60 * 24;
  const day = Math.floor(diff / oneDay);
  const state = (day / 365) * 100;

  return Number.parseFloat(state.toPrecision(digits));
};


export const DataProcessingUtils = {
  flattenNestedObjects,
  processStateOfIntervalHours,
  processLeftIntervalHours,
  processStateOfIntervalYears,
  processLeftIntervalYears,
};
