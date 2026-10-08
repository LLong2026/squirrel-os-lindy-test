function drainQueue(queue, limit) {
  let drained = 0;
  while (queue.length > 0 && drained < limit) {
    const item = queue.shift();
    if (item.retry) {
      queue.push(item);
    } else {
      drained++;
    }
  }
  return drained;
}
