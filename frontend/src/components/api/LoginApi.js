const mocks = {
  auth: { POST: { token: 'This-is-a-mocked-token' } },
  'user/me': { GET: { name: 'doggo', title: 'sir' } },
};

const apiCall = ({ url, data, method }) => new Promise((resolve, reject) => {
  setTimeout(() => {
    try {
      if (data.username !== process.env.VUE_APP_USER
        || data.password !== process.env.VUE_APP_SECRET) {
        reject(new Error(401));
      } else {
        resolve(mocks[url][method || 'GET']);
      }
    } catch (err) {
      reject(new Error(err));
    }
  }, 1000);
});

export default apiCall;
