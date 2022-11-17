// CPP program to create an empty vector
// and push values one by one.
#include <iostream>
#include <vector>
class bot{
	int x, y;
	public:
	bot(int x, int y):x(x), y(y){}
	void update(){
		x += 1;
		y += 1;
	}
	void print(){
		std::cout<<"("<<x<<","<<y<<")";
	}
};

int main()
{
	vector<bot> bots(3);
	// int x = 1, y=1;
	// (x, y) = (5, 1);
	// std::cout<<x;
	for(int i =0; i<3;++i){
		;
		a.update();
		
	}
	return 0;
}


// int main()
// {
// 	bot a(1, 10);
// 	// int x = 1, y=1;
// 	// (x, y) = (5, 1);
// 	// std::cout<<x;
// 	for(int i =0; i<3;++i){
// 		a.print();
// 		a.update();
		
// 	}
// 	return 0;
// }



// Create an empty vector
	// std::vector<int> vect;

	// vect.push_back(10);
	// vect.push_back(20);
	// vect.push_back(30);

	// for (int x : vect)
	// 	std::cout << x << " ";

	// return 0;
