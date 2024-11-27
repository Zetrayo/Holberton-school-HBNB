/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    const loginLink = document.getElementById('login-link'); // Replace with your login link's actual ID or selector
    const token = getCookie('access_token'); // Replace 'jwt_token' with the actual name of your JWT cookie

    if (token) {
        if (loginLink) {
            loginLink.style.display = 'none';
        }
    } else {
        if (loginLink) {
            loginLink.style.display = 'block';
        }
    }
});


function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}
