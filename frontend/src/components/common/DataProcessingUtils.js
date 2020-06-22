

const flattenNestedObjects = (inputObject) => {
  const outputArray = [];
  for (let i = 0; i < Object.keys(inputObject).length; i += 1) {
    outputArray.push(
      Object.assign(Object.values(inputObject)[i], {name: Object.keys(inputObject)[i]}),
    );
  }
  return outputArray;
};


export const DataProcessingUtils = {
  flattenNestedObjects,
};
