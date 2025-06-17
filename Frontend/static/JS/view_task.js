async function fetchTask() {
  try {
      const params = new URLSearchParams(window.location.search);
      const taskId = params.get("id");
      if (!taskId) {
        console.error("No se encontró ID en la URL");
      }
      const response = await fetch(`https://gestor-de-tareas-r39h.onrender.com/tasks/me/view/${taskId}`, {
        headers: {
          Authorization: `Bearer ${token}`
        },
        method: 'GET',
      })
      if (!response.ok) {
        console.error("No se encontró la tarea con el ID proporcionado");
        window.location.href = "taskify"; // Redirigir a la página principal si no se encuentra la tarea
        return;
      }
      const task = await response.json()
      
      {
        console.log("Tarea:", task);
        document.getElementById('task-title').value = task["title"]
        document.getElementById('task-subtitle').value = task["subtitle"]
        document.getElementById('task-description').value = task["description"]
        document.getElementById('task-priority').value = task["priority"]
        document.getElementById('task-description').value = task["description"]
        document.getElementById('task-status').value = task["status"]
      }

    } catch(error) {

          window.location.href = "taskify"; // Redirigir a la página principal si hay un error
        }
}
const errorMsg = document.getElementById("error-msg");
errorMsg.classList.add("hidden"); // ocultar mensaje anterior
fetchTask();

document.getElementById('task-updated').addEventListener('submit', async function(event) {
  event.preventDefault();

  const title = document.getElementById('task-title').value;
  const subtitle = document.getElementById('task-subtitle').value;
  const description = document.getElementById('task-description').value;
  const priority = document.getElementById('task-priority').value;
  const status = document.getElementById('task-status').value;

  const params = new URLSearchParams(window.location.search);
  const taskId = params.get("id");

  const taskData = {
    id: taskId,
    title: title,
    subtitle: subtitle,
    description: description,
    priority: priority,
    status: status
  };

  try {
    const response = await fetch(`https://gestor-de-tareas-r39h.onrender.com/tasks`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(taskData)
    });

    if (!response.ok) {
      throw new Error('Hubo un error al actualizar la tarea');
    }

    const data = await response.json();
    console.log('Tarea actualizada:', data);
    document.getElementById('success-msg').textContent = "Tarea actualizada correctamente";
    document.getElementById('success-msg').classList.remove("hidden");
    document.getElementById('volver').textContent=("🔙 Volver a Mis Tareas");
    document.getElementById('volver').classList.remove("hidden");
  } catch (error) {
    console.error('Error:', error);
    document.getElementById('error-msg').textContent = "Error al actualizar la tarea";
    document.getElementById('error-msg').classList.remove("hidden");
  }
});

document.getElementById('delete-task').addEventListener("click", async function(event) {
  event.preventDefault();

  const params = new URLSearchParams(window.location.search);
  const taskId = params.get("id");
  if (!taskId) {
    console.error("No se encontró ID en la URL");
    return;
  }
  try {
    const response = await fetch(`https://gestor-de-tareas-r39h.onrender.com/tasks/me/${taskId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('Hubo un error al eliminar la tarea');
    }

    document.getElementById('success-msg').textContent = "Tarea eliminada correctamente";
    document.getElementById('success-msg').classList.remove("hidden");
    document.getElementById('volver').textContent=("🔙 Volver a Mis Tareas");
    document.getElementById('volver').classList.remove("hidden");
  } catch (error) {
    console.error('Error:', error);
    document.getElementById('error-msg').textContent = "Error al eliminar la tarea";
    document.getElementById('error-msg').classList.remove("hidden");
  }
});
