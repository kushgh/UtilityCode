#include<iostream>
#include<vector>
#include<queue>
#include<algorithm>
#include<utility>

using namespace std;

class node{
    public:
    int data;
    vector<node*>child;
};

node* new_node(int data){
    node* n = new node();
    n->data = data;
    vector<node*>vec(3,NULL);
    n->child = vec;

    return n;

}


    node* insert_value(node* &root, int my_value){
        queue<node*> q;
        q.push(root);
        int n = 0;
    
        while(!q.empty()){
             node* parent = q.front();
             cout<<parent->data<<endl;
             q.pop();
             for(int i = 0; i < 3;i++){
                if(parent->child[i]!=NULL){
                    q.push(parent->child[i]);
                    cout<<parent->child[i]->data<<" ";
                }
                else{
                    parent->child[i] = new_node(my_value);
                    q.push(parent->child[i]);
                    cout<<"i"<<parent->child[i]->data<<" ";
                    return 0;
                }
             }
                cout<<endl;
        }
    }
int main(){

    node* root = new_node(1);
    insert_value(root,2);
    cout<<"..............."<<endl;
    insert_value(root,3);
   cout<<"..............."<<endl;
    insert_value(root,4);
    cout<<"..............."<<endl;
    insert_value(root,5);
    cout<<"..............."<<endl;
    insert_value(root,6);
    cout<<"..............."<<endl;
    insert_value(root,7);
     cout<<"..............."<<endl;
    insert_value(root,8);
    return 0;
}