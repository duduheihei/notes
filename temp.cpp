int cmpVehicleWithTrajectory(const void* a, const void* b) {
	AdasObjectVac obj_a = *(AdasObjectVac*)a;
	AdasObjectVac obj_b = *(AdasObjectVac*)b;
	
	MFloat xa = obj_a.f32LatDistance;
	MFloat ya = obj_a.f32LongDistance;
	MFloat xb = obj_b.f32LatDistance;
	MFloat yb = obj_b.f32LongDistance;
	MFloat xaRefer = 0.5 * f32AdasCurvature * ya * ya;
	MFloat xbRefer = 0.5 * f32AdasCurvature * yb * yb;
	MFloat diffA = fabs(xa - xaRefer);
	MFloat diffB = fabs(xb - xbRefer);
	// in current main path, nearly 3m from shi yunpeng
	if ((diffA <= 1.8) && (diffB <= 1.8)) {
		if (ya > yb) {
			return 1;
		}
		else {
			return -1;
		}
	}

	if (diffA > diffB) {
		return 1;
	}
	else {
		return -1;
	}
}

MVoid postCIPV(AdasInnerCarInitInfo* carInfo, AdasDynamicInput* adasDynamicInput, AdasOutput* adasOutput) {
	MFloat speedVeh = adasDynamicInput->carSignal.f32VehicleSpeed/3.6;
	MFloat wheelBase = carInfo->s32CarWheelBase;
	MFloat yawRate = adasDynamicInput->carSignal.vehicleIMU[adasDynamicInput->carSignal.s32vehicleIMUSize - 1].f32YawRate;
	MFloat steerAngle = adasDynamicInput->carSignal.f32SteerAngle;
	MFloat curvatureLowSpeed = steerAngle / wheelBase;
	MFloat curvatureHighSpeed = yawRate / speedVeh;
	if (speedVeh<=1)
	{
		f32AdasCurvature = curvatureLowSpeed;
	}
	else if (speedVeh>=1.5)
	{
		f32AdasCurvature = curvatureHighSpeed;
	}
	else
	{
		f32AdasCurvature = (1.5-speedVeh)/0.5* curvatureLowSpeed + (speedVeh-1)/0.5* curvatureHighSpeed;
	}
	qsort(&(adasOutput->pObjectOutput->pObjects[0]), adasOutput->pObjectOutput->s32VehicleNum, sizeof(AdasObjectVac), cmpVehicleWithTrajectory);
	if (adasOutput->pObjectOutput->s32VehicleNum > 0) {
		MFloat x = adasOutput->pObjectOutput->pObjects[0].f32LatDistance;
		MFloat y = adasOutput->pObjectOutput->pObjects[0].f32LongDistance;
		if (fabs(adasOutput->pObjectOutput->pObjects[0].f32LatDistance-0.5*y*y*f32AdasCurvature) < 2.0) {
			adasOutput->pObjectOutput->pObjects[0].s32Cipv = 1;
		}
	}
}