

const incrementNumber = (inputNumber, increment, digits) => {
  return Number(Number(parseFloat(inputNumber) + increment, ).toFixed(digits));
};
const decrementNumber = (inputNumber, increment, digits) => {
  return Number(Number(parseFloat(inputNumber) - increment, ).toFixed(digits));
};
const initObject = (inputObject, initValue) => {
  Object.keys(inputObject).forEach((index) => inputObject[index] = initValue);
};
const indexOfObjectValueInArray = (arrayOfObjects, value) => {
  for (let i = 0; i < arrayOfObjects.length; i += 1) {
    if (Object.values(arrayOfObjects[i]).includes(value)) {
      return i;
    }
  }
};


export const FormUtils = {
  incrementNumber,
  decrementNumber,
  initObject,
  indexOfObjectValueInArray,
};
