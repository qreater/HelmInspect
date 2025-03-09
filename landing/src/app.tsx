import React from 'react'

import { Navigate, Route, Routes } from 'react-router'
import { BrowserRouter } from 'react-router-dom'

import Layout from './components/layout/layout'
import { Landing } from './containers/landing/landing'
import { Why } from './containers/why/why'
import { How } from './containers/how/how'

const App: React.FC = () => {
    return (
        <>
            <BrowserRouter>
                <Layout>
                    <Routes>
                        <Route
                            path="/"
                            element={
                                <>
                                    <Landing />
                                    <Why />
                                    <How />
                                </>
                            }
                        />
                        <Route path="*" element={<Navigate to="/" replace />} />
                    </Routes>
                </Layout>
            </BrowserRouter>
        </>
    )
}

export default App
