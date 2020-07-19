/* eslint-disable import/prefer-default-export */
export const apiGetLocation = () => new Promise((resolve, reject) => {
  setTimeout(() => {
    try {
      if (!('geolocation' in navigator)) {
        const error = 'Geolocation is not available!';
        console.error(error);
        reject(new Error(error));
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
