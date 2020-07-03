/* eslint-disable import/prefer-default-export */
export const apiGetLocation = () => new Promise((resolve, reject) => {
  if (!('geolocation' in navigator)) {
    reject(console.error('Geolocation is not available.'));
  } else {
    navigator.geolocation.getCurrentPosition((pos) => resolve(pos),
      (error) => reject(console.error(error)));
  }
});
