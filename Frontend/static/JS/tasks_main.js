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
        const now = Math.floor(Date.now() / 1000);
        return payload.exp < now;
      }

      if (!token || isTokenExpired(token)) {
        console.log("Token inválido o expirado");
        window.location.href = "login.html";
      } else {
        
        fetchTasks();
      }

      async function fetchTasks() {
        try {
          const response = await fetch('https://gestor-de-tareas-r39h.onrender.com/tasks/me', {
            headers: {
              'Authorization': `Bearer ${token}`
            },
            method: 'GET',
          });

          if (!response.ok) {
            throw new Error('No se pudieron obtener las tareas');
          }

          const tasks = await response.json();
          renderTasks(tasks);
        } catch (error) {
          console.error('Error al buscar las tareas:', error);
        }
      }

      function renderTasks(tasks) {
        const tbody = document.querySelector("tbody");
        tbody.innerHTML = ""; // limpiar tareas actuales
        tasks.forEach(task => {
          const tr = document.createElement("tr");
          tr.className = "border-t border-t-[#2f396a]";

          tr.innerHTML = `
            <td class="cursor-pointer hover:underline table-...-120 h-[72px] px-4 py-2 w-[400px] text-white text-sm font-normal leading-normal">
              <a href="view_task.html?id=${task.id}">${task.title || 'Sin título'}</a>
            </td>
            <td class="table-...-240 h-[72px] px-4 py-2 w-60 text-sm font-normal leading-normal">
              <button class="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-8 px-4 bg-[#21284a] text-white text-sm font-medium leading-normal w-full">
                <span class="truncate">${task.subtitle || 'Sin subtítulo'}</span>
              </button>
            </td>
            <td class="table-...-240 h-[72px] px-4 py-2 w-60 text-sm font-normal leading-normal">
              <button class="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-8 px-4 bg-[#21284a] text-white text-sm font-medium leading-normal w-full">
                <span class="truncate">${task.priority || 'Media'}</span>
              </button>
            </td>
            <td class="table-...-360 h-[72px] px-4 py-2 w-60 text-sm font-normal leading-normal">
              <button class="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-8 px-4 bg-[#21284a] text-white text-sm font-medium leading-normal w-full">
                <span class="truncate">${task.status || 'Pendiente'}</span>
              </button>
            </td>
            <td class="table-...-480 h-[72px] px-4 py-2 w-[400px] text-[#8e99cc] text-sm font-normal leading-normal">
              ${task.due_date || 'Sin fecha'}
            </td>
            <td class="table-...-600 h-[72px] px-4 py-2 w-[400px] text-[#8e99cc] text-sm font-normal leading-normal">
              ${task.assignee || 'Anónimo'}
            </td>
          `;

          tbody.appendChild(tr);
        });
      }