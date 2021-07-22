% MATLAB's basic datatype is a vector
a = [1,2,3,4]
b = 2*a

% MATLAB looping syntax needs `end`
for c = ['q','u','v']
disp(['c: ', c]);
end

% MATLAB can create vectors with colons, and indexing starts with 1
x = 0:2:999;
y = sin(2*pi*x/250);
z = (x/100).^2;

disp(['x(1) = ', num2str(x(1))]);
disp(['x(end) = ', num2str(x(1))]);
disp(['length(x) = ', num2str(length(x))]);

% MATLAB uses built-in functions
figure;
subplot(2,1,1); plot(x,y);
subplot(2,1,2); plot(x,z);