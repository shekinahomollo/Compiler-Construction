int limit;
int current;
int sum;

limit = 10;
current = 0;
sum = 0;

while (current < limit) {
    if (current == 5) {
        sum = sum + 10;
    }
    else {
        sum = sum + current;
    }
    current = current + 1;
}