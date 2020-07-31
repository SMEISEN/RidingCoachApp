/* eslint-disable import/prefer-default-export */
const mocks = {
  auth: { POST: { token: 'This-is-a-mocked-token' } },
  'user/me': { GET: { name: 'doggo', title: 'sir' } },
};

export const apiLogin = ({ url, data, method }) => new Promise((resolve, reject) => {
  setTimeout(() => {
    try {
      if (data.username !== process.env.VUE_APP_USER
        || data.password !== process.env.VUE_APP_SECRET) {
        reject(new Error('Request failed with status code 401!'));
      } else {
        resolve(mocks[url][method || 'GET']);
      }
    } catch (error) {
      console.error(error);
      reject(new Error(error));
    }
  }, 15000);
});
