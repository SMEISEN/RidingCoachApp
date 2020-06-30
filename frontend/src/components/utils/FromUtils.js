/* eslint no-return-assign: "off" */
/* eslint no-param-reassign: "off" */
/* eslint-disable import/prefer-default-export */

export const incrementNumber = (inputNumber, increment, digits) => Number(
  Number(parseFloat(inputNumber) + increment).toFixed(digits),
);
export const decrementNumber = (inputNumber, increment, digits) => Number(
  Number(parseFloat(inputNumber) - increment).toFixed(digits),
);
export const initObject = (inputObject, initValue) => {
  Object.keys(inputObject).forEach((index) => inputObject[index] = initValue);
};
export const indexOfObjectValueInArray = (arrayOfObjects, value) => {
  for (let i = 0; i < arrayOfObjects.length; i += 1) {
    if (Object.values(arrayOfObjects[i]).includes(value)) {
      return i;
    }
  }
  return new Error('value not found!');
};
