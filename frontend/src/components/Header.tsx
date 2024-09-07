'use client'

import { useState } from 'react'
import Logo from './ui/Logo'
import NavLink from './ui/NavLink'
import SearchBar from './ui/SearchBar'

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <header className="bg-surface shadow-sm">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Logo />
        <div className="flex-grow max-w-xl mx-4 hidden md:block">
          <SearchBar />
        </div>
        <nav className="hidden md:flex space-x-4">
          <NavLink href="/">Home</NavLink>
          <NavLink href="/about">About</NavLink>
          <NavLink href="/contact">Contact</NavLink>
        </nav>
        <button 
          className="md:hidden"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          Menu
        </button>
      </div>
      {mobileMenuOpen && (
        <div className="md:hidden">
          <SearchBar />
          <nav className="flex flex-col space-y-2 mt-4">
            <NavLink href="/">Home</NavLink>
            <NavLink href="/about">About</NavLink>
            <NavLink href="/contact">Contact</NavLink>
          </nav>
        </div>
      )}
    </header>
  )
}
