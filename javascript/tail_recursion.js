//  nth term of fibonacci series using tail recursion
let a = 0;
let b = 1;

let n = Number(prompt ("Enter the  nth term "));

console.log(fib(n,a,b));

function fib(n,a,b){
    if(n==0)
        return a;
    
    return fib(n-1,b,a+b);
}
