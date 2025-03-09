import Navbar from '../navbar/navbar'
import { LayoutWrapper, LayoutContent } from './layout.styles'

interface LayoutProps {
    children: React.ReactNode
}

const Layout = ({ children }: LayoutProps) => {
    return (
        <LayoutWrapper>
            <Navbar />
            <LayoutContent>{children}</LayoutContent>
        </LayoutWrapper>
    )
}

export default Layout
