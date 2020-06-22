

const incrementNumber = (inputNumber, increment, digits) => {
  return Number(parseFloat(inputNumber) + increment, ).toFixed(digits);
};
const decrementNumber = (inputNumber, increment, digits) => {
  return Number(parseFloat(inputNumber) - increment, ).toFixed(digits);
};
const initObject = (inputObject, initValue) => {
  Object.keys(inputObject).forEach((index) => inputObject[index] = initValue);
};


export const FormUtils = {
  incrementNumber,
  decrementNumber,
  initObject,
};
