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
    if (target > arraySorted[arraySorted.length - 1][0]) {
      return [arraySorted[arraySorted.length - 2], arraySorted[arraySorted.length - 1]];
    }
    return arraySorted
      .sort((a, b) => Math.abs(a[0] - target) - Math.abs(b[0] - target)).slice(0, 2);
  }
  const nearestXY = getNearest(targetX, arrayXY);
  const xDiff = nearestXY[1][0] - nearestXY[0][0];
  const yDiff = nearestXY[1][1] - nearestXY[0][1];
  return nearestXY[0][1] + (yDiff / xDiff) * (targetX - nearestXY[0][0]);
};
