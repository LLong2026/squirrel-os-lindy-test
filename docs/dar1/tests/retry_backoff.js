function retryWithBackoff(tasks, maxRetries) {
  let attempts = 0;
  let done = 0;
  let pending = tasks;
  while (pending.length > 0 && attempts < maxRetries) {
    const task = pending.shift();
    if (task.failed) {
      attempts++;
    } else {
      done++;
    }
  }
  return done;
}
