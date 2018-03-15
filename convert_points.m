R = rotationMatrix;
R1 = inv(R);
T = translationVector;

xim = 1224,2201;
yim = 40;

cx = cameraParams.IntrinsicMatrix(3,1);
cy = cameraParams.IntrinsicMatrix(3,2);
sx = 30/193;
sy = 30/190;

fx = (cameraParams.IntrinsicMatrix(1,1))/sx;
fy = (cameraParams.IntrinsicMatrix(2,2))/sy;

fx;
fy;
f = (fx+fy)/2;
f;

xc = (xim - cx)/sx;
yc = (yim - cy)/sy;
zc = f;

C = [xc;yc;zc];


W = R1*(C -T);
xw = W(1,1);
yw = W(2,1);
zw = W(3,1);

xw;
yw;
zw;

x = [xw;yw;zw];





