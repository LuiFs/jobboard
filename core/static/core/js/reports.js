fetch('/reports/json/')
  .then(r => r.json())
  .then(data => {
    const jobs = data.jobs;
    const apps = data.applications;
    const labels = Array.from(new Set(jobs.map(j=>j.month).concat(apps.map(a=>a.month)))).sort();

    const jobsCount = labels.map(l => (jobs.find(j=>j.month===l)||{count:0}).count);
    const appsCount = labels.map(l => (apps.find(a=>a.month===l)||{count:0}).count);

    new Chart(document.getElementById('jobsChart'), {
      type: 'bar',
      data: {labels: labels, datasets: [{label: 'Vagas por mês', data: jobsCount}]},
    });

    new Chart(document.getElementById('appsChart'), {
      type: 'line',
      data: {labels: labels, datasets: [{label: 'Candidatos por mês', data: appsCount}]},
    });
  });
