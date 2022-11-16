// CPP program to create an empty vector
// and push values one by one.
#include <iostream>
#include <vector>

int main()
{
	// Create an empty vector
	std::vector<int> vect;

	vect.push_back(10);
	vect.push_back(20);
	vect.push_back(30);

	for (int x : vect)
		std::cout << x << " ";

	return 0;
}
