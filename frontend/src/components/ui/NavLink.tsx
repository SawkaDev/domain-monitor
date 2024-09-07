import Link from 'next/link'

export default function NavLink({ href, children }: { href: string; children: React.ReactNode }) {
  return (
    <Link href={href} className="text-text-secondary hover:text-primary transition-colors">
      {children}
    </Link>
  )
}
