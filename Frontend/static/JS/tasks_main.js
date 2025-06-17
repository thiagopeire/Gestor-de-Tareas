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
fetchTasks(); 

function renderTasks(tasks) {
  const tbody = document.querySelector("tbody");
  tbody.innerHTML = ""; // limpiar tareas actuales
  tasks.forEach(task => {
    const tr = document.createElement("tr");
    tr.className = "border-t border-t-[#2f396a]";

    tr.innerHTML = `
      <td class="cursor-pointer hover:underline table-...-120 h-[72px] px-4 py-2 w-[400px] text-white text-sm font-normal leading-normal">
        <a href="/${task.id}">${task.title || 'Sin título'}</a>
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
        ${task.expired_at || 'Sin fecha'}
      </td>
      <td class="table-...-600 h-[72px] px-4 py-2 w-[400px] text-[#8e99cc] text-sm font-normal leading-normal">
        ${task.assignee || 'Anónimo'}
      </td>
    `;

    tbody.appendChild(tr);
  });
}