import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
from sklearn.neighbors import KDTree

def run_analysis(calculate_torus_stresses, fatigue_analysis, advanced_calculations, create_advanced_animation):
    print("3D Finite Element Analysis")

    # Get user input for parameters
    R = float(input("Enter major radius (R): "))
    r = float(input("Enter minor radius (r): "))
    t = float(input("Enter thickness (t): "))
    E = float(input("Enter Young's modulus (E): "))
    nu = float(input("Enter Poisson's ratio (nu): "))
    p_int = float(input("Enter internal pressure (p_int): "))
    p_ext = float(input("Enter external pressure (p_ext): "))
    n_elements = int(input("Enter number of elements: "))

    # Generate mesh
    nodes, elements = generate_torus_mesh(R, r, t, n_elements)

    # Assemble global stiffness matrix and force vector
    K, F = assemble_system(nodes, elements, E, nu, p_int, p_ext)

    # Solve system
    U = solve_system(K, F)

    # Post-process results
    stresses, strains = post_process(nodes, elements, U, E, nu)

    # Display results
    print("\nFEM Analysis Results:")
    print(f"Max displacement: {np.max(np.abs(U)):.4e}")
    print(f"Max von Mises stress: {np.max(stresses):.4e}")
    print(f"Max strain: {np.max(strains):.4e}")

    # Visualize results
    create_advanced_animation(nodes, elements, U, stresses)

    input("\nPress Enter to return to the main menu...")

def generate_torus_mesh(R, r, t, n):
    theta = np.linspace(0, 2*np.pi, n)
    phi = np.linspace(0, 2*np.pi, n)
    rho = np.linspace(r - t/2, r + t/2, 3)  # 3 layers for thickness
    theta, phi, rho = np.meshgrid(theta, phi, rho)
    
    x = (R + rho*np.cos(phi)) * np.cos(theta)
    y = (R + rho*np.cos(phi)) * np.sin(theta)
    z = rho * np.sin(phi)
    
    nodes = np.vstack((x.ravel(), y.ravel(), z.ravel())).T
    
    elements = []
    for i in range(n-1):
        for j in range(n-1):
            for k in range(2):
                element = [
                    i*n*3 + j*3 + k,
                    i*n*3 + j*3 + k + 1,
                    (i+1)*n*3 + j*3 + k + 1,
                    (i+1)*n*3 + j*3 + k,
                    i*n*3 + j*3 + k + 3,
                    i*n*3 + j*3 + k + 4,
                    (i+1)*n*3 + j*3 + k + 4,
                    (i+1)*n*3 + j*3 + k + 3
                ]
                elements.append(element)
    
    return nodes, np.array(elements)

def assemble_system(nodes, elements, E, nu, p_int, p_ext):
    n_nodes = len(nodes)
    n_elements = len(elements)
    
    # Initialize global stiffness matrix and force vector
    K = np.zeros((3*n_nodes, 3*n_nodes))
    F = np.zeros(3*n_nodes)
    
    # Element stiffness matrix for 8-node hexahedral element
    D = E / ((1 + nu) * (1 - 2*nu)) * np.array([
        [1-nu, nu, nu, 0, 0, 0],
        [nu, 1-nu, nu, 0, 0, 0],
        [nu, nu, 1-nu, 0, 0, 0],
        [0, 0, 0, (1-2*nu)/2, 0, 0],
        [0, 0, 0, 0, (1-2*nu)/2, 0],
        [0, 0, 0, 0, 0, (1-2*nu)/2]
    ])
    
    for el in elements:
        el_nodes = nodes[el]
        J = el_nodes[1:] - el_nodes[0]
        det_J = np.linalg.det(J)
        B = np.zeros((6, 24))
        
        for i in range(8):
            dN = np.array([
                [(-1)**(i+1), 0, 0],
                [0, (-1)**((i//2)+1), 0],
                [0, 0, (-1)**((i//4)+1)]
            ]) / 8
            B_i = np.zeros((6, 3))
            B_i[:3, :] = dN
            B_i[3:, :] = dN[[1,2,0], :]
            B[:, 3*i:3*(i+1)] = B_i
        
        k_el = det_J * B.T @ D @ B
        
        for i in range(8):
            for j in range(8):
                K[3*el[i]:3*(el[i]+1), 3*el[j]:3*(el[j]+1)] += k_el[3*i:3*(i+1), 3*j:3*(j+1)]
        
        # Apply pressure loads
        for face in range(6):
            face_nodes = el[face_connectivity[face]]
            face_center = np.mean(nodes[face_nodes], axis=0)
            normal = face_normals[face]
            pressure = p_int if np.dot(face_center - nodes[el[0]], normal) > 0 else p_ext
            F[3*face_nodes] += pressure * normal[0] * det_J / 4
            F[3*face_nodes+1] += pressure * normal[1] * det_J / 4
            F[3*face_nodes+2] += pressure * normal[2] * det_J / 4
    
    return csr_matrix(K), F

def solve_system(K, F):
    # Apply boundary conditions (fix some nodes)
    fixed_dofs = np.arange(3)  # Fix first node for simplicity
    free_dofs = np.setdiff1d(np.arange(K.shape[0]), fixed_dofs)
    
    # Solve the system
    U_free = spsolve(K[free_dofs][:, free_dofs], F[free_dofs])
    
    # Reconstruct full displacement vector
    U = np.zeros(K.shape[0])
    U[free_dofs] = U_free
    
    return U

def post_process(nodes, elements, U, E, nu):
    n_elements = len(elements)
    stresses = np.zeros((n_elements, 6))
    strains = np.zeros((n_elements, 6))
    
    D = E / ((1 + nu) * (1 - 2*nu)) * np.array([
        [1-nu, nu, nu, 0, 0, 0],
        [nu, 1-nu, nu, 0, 0, 0],
        [nu, nu, 1-nu, 0, 0, 0],
        [0, 0, 0, (1-2*nu)/2, 0, 0],
        [0, 0, 0, 0, (1-2*nu)/2, 0],
        [0, 0, 0, 0, 0, (1-2*nu)/2]
    ])
    
    for i, el in enumerate(elements):
        el_nodes = nodes[el]
        J = el_nodes[1:] - el_nodes[0]
        B = np.zeros((6, 24))
        
        for j in range(8):
            dN = np.array([
                [(-1)**(j+1), 0, 0],
                [0, (-1)**((j//2)+1), 0],
                [0, 0, (-1)**((j//4)+1)]
            ]) / 8
            B_j = np.zeros((6, 3))
            B_j[:3, :] = dN
            B_j[3:, :] = dN[[1,2,0], :]
            B[:, 3*j:3*(j+1)] = B_j
        
        el_U = U[np.repeat(3*el, 3) + np.tile(np.arange(3), 8)]
        strains[i] = B @ el_U
        stresses[i] = D @ strains[i]
    
    return stresses, strains

# Face connectivity and normals for hexahedral elements
face_connectivity = [
    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [0, 1, 5, 4],
    [1, 2, 6, 5],
    [2, 3, 7, 6],
    [3, 0, 4, 7]
]

face_normals = [
    [0, 0, -1],
    [0, 0, 1],
    [0, -1, 0],
    [1, 0, 0],
    [0, 1, 0],
    [-1, 0, 0]
]

if __name__ == "__main__":
    from main import calculate_torus_stresses, fatigue_analysis
    from modules import advanced_calculations
    from visualization import create_advanced_animation
    run_analysis(calculate_torus_stresses, fatigue_analysis, advanced_calculations, create_advanced_animation)
