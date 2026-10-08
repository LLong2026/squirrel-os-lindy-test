function twoLoops(a) {
  while (a.length > 0) { a.shift(); }
  while (a.length > 0) { a.shift(); }
  return a;
}
