import Link from 'next/link'

export default function NavLink({ href, children }: { href: string; children: React.ReactNode }) {
  return (
    <Link href={href} className="text-gray-600 hover:text-blue-500 transition-colors">
      {children}
    </Link>
  )
}
