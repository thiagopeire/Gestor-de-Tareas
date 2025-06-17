const token = localStorage.getItem('access_token');
    function parseJwt(token) {
  if (!token) return null;
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(c =>
      '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
    ).join(''));
    return JSON.parse(jsonPayload);
  } catch (e) {
    return null;
  }
}
function isTokenExpired(token) {
  const payload = parseJwt(token);
  if (!payload || !payload.exp) return true;

  const now = Math.floor(Date.now() / 1000); // tiempo actual en segundos
  return payload.exp < now;
}
if (!token || isTokenExpired(token)) {
  console.log("Token inválido o expirado");
  // podés redirigir al login
  window.location.href = "login.html";
}