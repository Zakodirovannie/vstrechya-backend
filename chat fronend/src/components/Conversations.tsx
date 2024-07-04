import { useContext, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";
import axios from "axios";

interface UserResponse {
  id: string;
  first_name: string;
  url: string;
}

export function Conversations() {
  const { user } = useContext(AuthContext);
  const [users, setUsers] = useState<UserResponse[]>([]);

  useEffect(() => {
    async function fetchUsers() {
      const res = await fetch("http://127.0.0.1:8000/users/all/", {
        headers: {
          Authorization: `Bearer ${user?.token}`,
        },
      });
      const data = await res.json();
      setUsers(data);
    }
    fetchUsers();
  }, [user]);

  function createConversationName(username: string) {
    const namesAlph = [user?.id, username].sort();
    return `${namesAlph[0]}__${namesAlph[1]}`;
  }

  return (
    <div>
      {users
        .filter((u) => u.id !== user?.id)
        .map((u) => (
          <Link
            key={u.id}
            to={`chats/${createConversationName(u.id)}`}
          >
            <div className="flex items-center justify-items-center gap-2 mb-3">
              <img className="w-10 h-10 rounded-full ring-2 ring-gray-300 dark:ring-gray-500 p-1" src="https://cdn.shopify.com/s/files/1/1648/6123/t/2/assets/blog-avatar.jpg?0" alt="" />
              <span className="subpixel-antialiased font-semibold text-grey-500">{u.first_name}</span>
            </div>
          </Link>
        ))}
    </div>
  );
}
