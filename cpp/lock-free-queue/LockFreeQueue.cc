// http://www.1024cores.net/home/lock-free-algorithms/queues/non-intrusive-mpsc-node-based-queue
template<typename T>
class MPSCQueue
{
    private:
        struct Node
        {
                Node* volatile next;
                T value;
                Node() :
                        next(0)
                {
                }
        };
        typedef Node* node_ptr;
        Node* volatile m_head;
        Node* m_tail;
    public:
        MPSCQueue() :
                m_head(0), m_tail(0)
        {
            m_head = new Node;
            m_tail = m_head;
        }
        void Push(T value)
        {
            /*
             * consider another way to avoid expensive new operation
             */
            Node* node = new Node;
            node->value = value;
            Node* prev = (Node*) atomic_get_and_set_vptr_t(
                    (vptr_t*) (&m_head), node);
            prev->next = node;
        }
        bool Pop(T& value)
        {
            Node* tail = m_tail;
            Node* next = tail->next;
            if (next)
            {
                m_tail = next;
                delete tail;
                value = next->value;
                return true;
            }
            return false;
        }
        ~MPSCQueue()
        {
            delete m_tail;
        }
};