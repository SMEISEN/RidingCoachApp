/* eslint-disable import/prefer-default-export */
export const apiGetLocation = () => new Promise((resolve, reject) => {
  setTimeout(() => {
    try {
      if (!('geolocation' in navigator)) {
        console.error('Geolocation is not available.');
        reject(new Error());
      } else {
        navigator.geolocation.getCurrentPosition((pos) => resolve(pos),
          (error) => {
            console.error(error);
            reject(error);
          });
      }
    } catch (error) {
      console.error(error);
      reject(new Error(error));
    }
  }, 5000);
});
