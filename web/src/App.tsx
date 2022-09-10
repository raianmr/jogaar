import axios from 'axios';
import { useState, useEffect } from 'react';

interface User {
  id: number
  email: string
}

export default function App() {
  const [users, setUsers] = useState<User[] | undefined>(undefined)
  useEffect(() => {
    axios.get("/users").then(res => setUsers(res.data))
  })

  return <>{
    users?.map((u, i) => <p key={i}>id-{u.id}: {u.email}</p>)
  }</>
}

