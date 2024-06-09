
function updateQueueStatus() {
    $.ajax({
        url: '/queue_status',
        type: 'POST',
        success: function(response) {
            // Assuming response has the structure {'message': {'total_queue': x, 'total_jobs': z}}
            if (response.message) {
                $('#total_queue').text(response.message.total_queue);           
                $('#total_jobs').text(response.message.total_finished_jobs);
            } else {
                console.log("Queue status is in progress");
            }
        },
        error: function(xhr) {
            console.error('Failed to fetch queue status');
        }
    });
}
function updateWorkerStatus() {
    $.ajax({
        url: '/worker_status',
        type: 'POST',
        success: function(response) {
            // Assuming response has the structure {'message': {'total_queue': x, 'total_jobs': z}}
            if (response.message) {                   
                $('#total_workers').text(response.message.total_workers);
            } else {
                console.log("Worker status is in progress");
            }
        },
        error: function(xhr) {
            console.error('Failed to fetch worker status');
        }
    });
}

// Call the updateQueueStatus function every 1 second
setInterval(updateQueueStatus, 5000);

// Call the updateQueueStatus function every 1 second
setInterval(updateWorkerStatus, 5000);