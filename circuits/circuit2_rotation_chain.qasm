OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
ry(pi/4) q[0];
rz(pi/6) q[1];
cx q[0],q[1];
ry(-pi/3) q[1];
cx q[1],q[0];