// Retire le sol capturé autour de l'objet scanné et recentre le modèle (Y vers le haut, posé en y=0).
import { NodeIO } from '@gltf-transform/core';
import { KHRONOS_EXTENSIONS } from '@gltf-transform/extensions';
import { prune, dedup } from '@gltf-transform/functions';

const [,, input, output, upAxisArg] = process.argv;
const io = new NodeIO().registerExtensions(KHRONOS_EXTENSIONS);
const doc = await io.read(input);
const root = doc.getRoot();
const node = root.listNodes().find(n => n.getMesh());
const mesh = node.getMesh();
const rot = node.getRotation(); // quaternion
// applique la rotation du nœud aux sommets pour travailler en coordonnées monde
function rotate(v, q) {
  const [x, y, z] = v, [qx, qy, qz, qw] = q;
  const ix = qw * x + qy * z - qz * y, iy = qw * y + qz * x - qx * z, iz = qw * z + qx * y - qy * x, iw = -qx * x - qy * y - qz * z;
  return [ix * qw + iw * -qx + iy * -qz - iz * -qy, iy * qw + iw * -qy + iz * -qx - ix * -qz, iz * qw + iw * -qz + ix * -qy - iy * -qx];
}
for (const prim of mesh.listPrimitives()) {
  const pos = prim.getAttribute('POSITION'), nor = prim.getAttribute('NORMAL');
  const idx = prim.getIndices();
  const n = pos.getCount();
  const P = new Float32Array(n * 3), N = nor ? new Float32Array(n * 3) : null;
  const v = [0, 0, 0];
  for (let i = 0; i < n; i++) {
    pos.getElement(i, v); const w = rotate(v, rot); P.set(w, i * 3);
    if (N) { nor.getElement(i, v); N.set(rotate(v, rot), i * 3); }
  }
  // histogramme des hauteurs (y) pour trouver le sol : tranche la plus peuplée près d'une extrémité
  let minY = Infinity, maxY = -Infinity;
  for (let i = 0; i < n; i++) { const y = P[i * 3 + 1]; if (y < minY) minY = y; if (y > maxY) maxY = y; }
  const bins = 100, h = new Array(bins).fill(0);
  for (let i = 0; i < n; i++) h[Math.min(bins - 1, Math.floor((P[i * 3 + 1] - minY) / (maxY - minY) * bins))]++;
  let best = 0; for (let b = 0; b < bins; b++) if (h[b] > h[best]) best = b;
  const floorY = minY + (best + 0.5) / bins * (maxY - minY);
  const height = maxY - minY;
  console.log('hauteur totale', height.toFixed(3), 'sol détecté à', floorY.toFixed(3), '(tranche', best, '/', bins, ', part', (h[best] / n * 100).toFixed(1) + '%)');
  const eps = height * 0.035;
  // triangles à garder : au moins un sommet nettement au-dessus du sol
  const I = idx.getArray();
  const keep = [];
  for (let t = 0; t < I.length; t += 3) {
    const a = I[t], b = I[t + 1], c = I[t + 2];
    const ya = P[a * 3 + 1], yb = P[b * 3 + 1], yc = P[c * 3 + 1];
    if (Math.max(ya, yb, yc) > floorY + eps) keep.push(a, b, c);
  }
  // sol dans le sens opposé (objet sous le sol) → inverser
  const above = keep.length, below = (() => { let k = 0; for (let t = 0; t < I.length; t += 3) { const ys = [P[I[t] * 3 + 1], P[I[t + 1] * 3 + 1], P[I[t + 2] * 3 + 1]]; if (Math.min(...ys) < floorY - eps) k += 3; } return k; })();
  let flip = false;
  if (below > above) { flip = true; keep.length = 0; for (let t = 0; t < I.length; t += 3) { const a = I[t], b = I[t + 1], c = I[t + 2]; if (Math.min(P[a * 3 + 1], P[b * 3 + 1], P[c * 3 + 1]) < floorY - eps) keep.push(a, b, c); } }
  console.log('triangles au-dessus du sol', keep.length / 3, '/', I.length / 3, flip ? '(objet sous le plan, axe inversé)' : '');
  // composantes connexes (sommets fusionnés par position, grille 1/300 de la hauteur) : on garde la plus grande
  const cell = height / 300, key = new Map(), parent = [];
  const find = (a) => { while (parent[a] !== a) { parent[a] = parent[parent[a]]; a = parent[a]; } return a; };
  const union = (a, b) => { a = find(a); b = find(b); if (a !== b) parent[a] = b; };
  const vid = new Int32Array(n);
  for (let i = 0; i < n; i++) { const k = Math.round(P[i*3]/cell) + ',' + Math.round(P[i*3+1]/cell) + ',' + Math.round(P[i*3+2]/cell); let id = key.get(k); if (id === undefined) { id = parent.length; parent.push(id); key.set(k, id); } vid[i] = id; }
  for (let t = 0; t < keep.length; t += 3) { union(vid[keep[t]], vid[keep[t+1]]); union(vid[keep[t+2]], vid[keep[t]]); }
  const count = new Map(); for (let t = 0; t < keep.length; t += 3) { const r = find(vid[keep[t]]); count.set(r, (count.get(r) || 0) + 1); }
  const comps = [...count.entries()].sort((a, b) => b[1] - a[1]);
  console.log('composantes', comps.length, 'principales', comps.slice(0, 5).map(c => c[1]).join(', '));
  const main = comps[0][0];
  // boîte de la composante principale
  let bm = [Infinity, Infinity, Infinity], bM = [-Infinity, -Infinity, -Infinity];
  for (let t = 0; t < keep.length; t += 3) if (find(vid[keep[t]]) === main) for (let j = 0; j < 3; j++) { const i = keep[t + j]; for (let k = 0; k < 3; k++) { bm[k] = Math.min(bm[k], P[i*3+k]); bM[k] = Math.max(bM[k], P[i*3+k]); } }
  const pad = [(bM[0]-bm[0])*0.08, (bM[1]-bm[1])*0.08, (bM[2]-bm[2])*0.08];
  const ok = new Set([main]);
  for (const [r, c] of comps.slice(1)) {
    if (c < comps[0][1] * 0.002) continue;
    let inside = true;
    for (let t = 0; t < keep.length && inside; t += 3) if (find(vid[keep[t]]) === r) for (let j = 0; j < 3 && inside; j++) { const i = keep[t + j]; for (let k = 0; k < 3; k++) if (P[i*3+k] < bm[k] - pad[k] || P[i*3+k] > bM[k] + pad[k]) { inside = false; break; } }
    if (inside) ok.add(r);
  }
  const kept2 = []; for (let t = 0; t < keep.length; t += 3) if (ok.has(find(vid[keep[t]]))) kept2.push(keep[t], keep[t+1], keep[t+2]);
  console.log('triangles après nettoyage', kept2.length / 3, '(composantes gardées', ok.size + ')');
  keep.length = 0; for (const i of kept2) keep.push(i);
  // remappe les sommets utilisés
  const map = new Map(); const NP = [], NN = [], NUV = [], NI = [];
  const uv = prim.getAttribute('TEXCOORD_0'); const uvv = [0, 0];
  for (const i of keep) {
    if (!map.has(i)) { map.set(i, NP.length / 3); NP.push(P[i * 3], P[i * 3 + 1], P[i * 3 + 2]); if (N) NN.push(N[i * 3], N[i * 3 + 1], N[i * 3 + 2]); if (uv) { uv.getElement(i, uvv); NUV.push(uvv[0], uvv[1]); } }
    NI.push(map.get(i));
  }
  let A = new Float32Array(NP);
  if (flip) for (let i = 0; i < A.length; i += 3) { A[i + 1] = -A[i + 1]; A[i + 2] = -A[i + 2]; }
  let B = N ? new Float32Array(NN) : null;
  if (flip && B) for (let i = 0; i < B.length; i += 3) { B[i + 1] = -B[i + 1]; B[i + 2] = -B[i + 2]; }
  // recentrage : x/z au centre, y min = 0
  let mn = [Infinity, Infinity, Infinity], mx = [-Infinity, -Infinity, -Infinity];
  for (let i = 0; i < A.length; i += 3) for (let k = 0; k < 3; k++) { mn[k] = Math.min(mn[k], A[i + k]); mx[k] = Math.max(mx[k], A[i + k]); }
  const cx = (mn[0] + mx[0]) / 2, cz = (mn[2] + mx[2]) / 2;
  for (let i = 0; i < A.length; i += 3) { A[i] -= cx; A[i + 1] -= mn[1]; A[i + 2] -= cz; }
  console.log('dimensions objet (unités scan) L', (mx[0] - mn[0]).toFixed(3), 'H', (mx[1] - mn[1]).toFixed(3), 'P', (mx[2] - mn[2]).toFixed(3));
  if (flip) { const I2 = NI; for (let t = 0; t < I2.length; t += 3) { const tmp = I2[t + 1]; I2[t + 1] = I2[t + 2]; I2[t + 2] = tmp; } }
  pos.setArray(A); if (B) nor.setArray(B);
  if (uv) uv.setArray(new Float32Array(NUV));
  idx.setArray(NI.length > 65535 ? new Uint32Array(NI) : new Uint16Array(NI));
}
node.setRotation([0, 0, 0, 1]);
await doc.transform(dedup(), prune());
await io.write(output, doc);
console.log('écrit', output);
