#include "setup.hpp"

void main_setup()
{ // mine
	const uint Width = 256u;
	const uint Length = 256u;
	const uint Height = 256u;

	const float sigma = 0.0003f;
	const float si_nu = 1E-32f;			// kinematic shear viscosity (water) [m^2/s]
	const float si_rho = 1E3f;			// density (water) [kg/m^3]
	const float si_sigma = 0.0001f; // surface tension (water) [kg/s^2] 0.072
	const float si_d = 4E-3f;				// bubble diameter [m]
	const float si_g = 9.81f;				// gravitational acceleration [m/s^2]
	const float si_f = units.si_f_from_si_g(si_g, si_rho);
	const float si_rho_particles = si_rho;
	const float rho = 1.0f;
	const float m = si_d / 64;									 // length si_x = x*[m]
	const float kg = si_rho / rho * cb(m);			 // density si_rho = rho*[kg/m^3]
	const float s = sqrt(sigma / si_sigma * kg); // velocity si_sigma = sigma*[kg/s^2]
	units.set_m_kg_s(m, kg, s);
	const float f = units.f(si_f);
	const float viscosity = units.nu(si_nu);

	// define simulation box size, viscosity and volume force
	LBM lbm(Width, Length, Height, viscosity, 0.0f, 0.0f, -f, sigma);

	// boeing
	const float size = Width / 1.5;
	const float3 center = float3(lbm.center().x, lbm.center().y, lbm.center().z);
	const float3x3 rotation = float3x3(float3(1, 0, 0), radians(0.0f));

	uchar *data = read_file_from_path(get_exe_path() + "../mesh_test.txt");
	lbm.voxelize_array_representation(data, center, rotation, size);

	// getN
	const ulong N = lbm.get_N();
	const uint Nx = lbm.get_Nx(), Ny = lbm.get_Ny(), Nz = lbm.get_Nz();

	// loop
	for (ulong n = 0ull; n < N; n++)
	{
		uint x = 0u, y = 0u, z = 0u;
		lbm.coordinates(n, x, y, z);
		// Geometry

		if (lbm.flags[n] != TYPE_S)
		{

			lbm.flags[n] = TYPE_G;

			float radius = 20.0f;

			if (z < 240 && z > 180 && x > Width / 2 - radius && x < Width / 2 + radius &&
					y > Length / 2 - radius && y < Length / 2 + radius)
			{
				lbm.flags[n] = TYPE_F; // make everything under height value fluidz>10u && z < Nz - 10u
															 // lbm.phi[n] = 1;
			}
		}

		if (x == 0u || x == Nx - 1u || y == 0u || y == Ny - 1u || z == 0u || z == Nz - 1u)
			lbm.flags[n] = TYPE_E;

		// if (z < 100 && z> 60 && x>10u && x < Nx - 10u && y>10u && y < Ny - 10u)
		//{
		//	lbm.flags[n] = TYPE_F; //make everything under height value fluidz>10u && z < Nz - 10u
		//	lbm.phi[n] = 1;
		// }
		// else {
		//	lbm.flags[n] = TYPE_G;
		//	lbm.phi[n] = 0;
		// }
		// if (z < 1.0f || y < 1.0f || x < 1.0f || x >(Width - 2.0f) || y >(Length - 2.0f)) {
		//	lbm.flags[n] = TYPE_S;
		// }
	}
	lbm.run();
}
