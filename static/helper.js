/**
 * Wrapper for fetch that appends the application url.
 * @param {string} query Route for fetch.
 * @return {Promise} Response for fetch.
 */
let callFetch = (query) => {
  return fetch('http://127.0.0.1:5000/' + query);
};
