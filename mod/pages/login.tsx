import Link from "next/link"
import styles from "../styles/Login.module.css"

export default function Home() {
  return (
    <div className={styles.container}>
      <Link href="/dashboard">login</Link>
    </div>
  )
}
