function healingLoop(system) {
  let state = system.initial;
  while (!system.healthy) {
    const anomaly = detect(state);
    state = isolate(state, anomaly);
    state = heal(state, anomaly);
    state = verify(state);
  }
  return state;
}
