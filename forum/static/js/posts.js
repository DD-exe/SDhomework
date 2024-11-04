// static/js/posts.js

const fetchPosts = () => {
    fetch('/api/posts/')
        .then(response => response.json())
        .then(data => {
            const postList = document.getElementById('post-list');
            postList.innerHTML = '';

            if (data.length === 0) {
                document.getElementById('no-posts').style.display = 'block';
            } else {
                document.getElementById('no-posts').style.display = 'none';
                data.forEach(post => {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <h3>${post.title}</h3>
                        <p>${post.content}</p>
                        <p>作者ID: ${post.user}</p>
                        <p>创建时间: ${new Date(post.created_at).toLocaleString()}</p>
                        <button onclick="handleDelete(${post.id})">删除</button>
                    `;
                    postList.appendChild(li);
                });
            }
        })
        .catch(error => console.error('Error fetching posts:', error));
};

const handleDelete = (postId) => {
    fetch(`/api/posts/${postId}/`, {
        method: 'DELETE',
    })
    .then(response => {
        if (response.ok) {
            fetchPosts(); // 刷新帖子列表
        } else {
            console.error('Error deleting post:', response);
        }
    })
    .catch(error => console.error('Error deleting post:', error));
};

document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname === '/PostList/') {
        fetchPosts(); // 加载帖子列表
    }

    if (window.location.pathname === '/NewPost/') {
        document.getElementById('new-post-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const newPost = {
                title: document.getElementById('title').value,
                content: document.getElementById('content').value,
                user: 1 // 假设用户ID为1
            };

            fetch('/api/posts/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newPost),
            })
            .then(response => {
                if (response.ok) {
                    window.location.href = '/PostList/'; // 成功后跳转
                } else {
                    console.error('Error creating post:', response);
                }
            })
            .catch(error => console.error('Error creating post:', error));
        });
    }
});
