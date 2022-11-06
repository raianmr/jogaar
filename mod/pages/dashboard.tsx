import Link from "next/link"
import styles from "../styles/Dashboard.module.css"

export default function Home() {
  return (
    <div className={styles.container}>
      <Link href="/">dashboard</Link>
    </div>
  )
}
