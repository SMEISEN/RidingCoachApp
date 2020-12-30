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
export const interpolateLinearly1D = (targetX, arrayXY) => {
  if (arrayXY.length === 0) {
    throw RangeError('Empty array was given!');
  }
  if (arrayXY.length === 1) {
    return arrayXY[0][1];
  }
  function getNearest(target, array) {
    const arraySorted = array.sort((a, b) => {
      if (a[0] === b[0]) {
        return 0;
      }
      return (a[0] < b[0]) ? -1 : 1;
    });
    if (target < arraySorted[0][0]) {
      return [arraySorted[0], arraySorted[1]];
    }
    if (target > arraySorted[-1][0]) {
      return [arraySorted[-2], arraySorted[-1]];
    }
    return arraySorted
      .sort((a, b) => Math.abs(a[0] - target) - Math.abs(b[0] - target)).slice(0, 2);
  }
  const nearestXY = getNearest(targetX, arrayXY);
  const xDiff = nearestXY[1][0] - nearestXY[0][0];
  const yDiff = nearestXY[1][1] - nearestXY[0][1];
  return nearestXY[0][1] + (yDiff / xDiff) * (targetX - nearestXY[0][0]);
};
