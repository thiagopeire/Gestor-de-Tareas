        document.getElementById('create_task').addEventListener('submit', async function(event) {
          event.preventDefault();

          const title = document.getElementById('task-title').value;
          const subtitle = document.getElementById('task-subtitle').value;
          const description = document.getElementById('task-description').value;
          const priority = document.getElementById('task-priority').value;
          const dueDate = document.getElementById('task-due-date').value;
          const taskData = {
            title: title,
            subtitle: subtitle,
            description: description,
            priority: priority,
            expired_at: dueDate !== '' ? dueDate : "En proceso"
          };
          console.log('Task Data:', taskData);
          try {
              const response = await fetch('https://gestor-de-tareas-r39h.onrender.com/tasks', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${token}`
              },
              body: JSON.stringify(taskData)
              });
                if (!response.ok) {
                    throw new Error('Hubo un error en la conexion');
                }
            document.getElementById('success-msg').textContent = "Tarea creada con exito";
            document.getElementById('success-msg').classList.remove("hidden");
            document.getElementById('volver').textContent=("🔙 Volver a Mis Tareas");
            document.getElementById('volver').classList.remove("hidden");

          } catch (error) {
                console.error('Error:', error);
                document.getElementById('error-msg').textContent = "Error al crear la tarea: " + error.message;
                document.getElementById('error-msg').classList.remove("hidden");
            }
        });